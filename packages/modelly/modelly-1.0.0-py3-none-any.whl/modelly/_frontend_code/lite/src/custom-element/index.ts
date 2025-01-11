// NOTE: We should only import the types from ".." to avoid the circular dependency of implementations,
// which causes repeated executions of the ".." module in †he dev mode and can lead to multiple instances of the dev app.
import type {
	create as createLiteAppFunc,
	Options,
	ModellyAppController
} from "..";
import { clean_indent } from "./indent";

interface ModellyComponentOptions {
	info: Options["info"];
	container: Options["container"];
	isEmbed: Options["isEmbed"];
	initialHeight?: Options["initialHeight"];
	eager: Options["eager"];
	themeMode: Options["themeMode"];
	autoScroll: Options["autoScroll"];
	controlPageTitle: Options["controlPageTitle"];
	appMode: Options["appMode"];
	sharedWorkerMode?: Options["sharedWorkerMode"];
}

interface ModellyLiteAppOptions {
	files?: Options["files"];
	requirements?: Options["requirements"];
	code?: Options["code"];
	entrypoint?: Options["entrypoint"];
}

function parseRequirementsTxt(content: string): string[] {
	return content
		.split("\n")
		.filter((r) => !r.startsWith("#"))
		.map((r) => r.trim())
		.filter((r) => r !== "");
}

export function bootstrap_custom_element(
	create: typeof createLiteAppFunc
): void {
	const CUSTOM_ELEMENT_NAME = "modelly-lite";

	if (customElements.get(CUSTOM_ELEMENT_NAME)) {
		return;
	}

	class ModellyLiteAppElement extends HTMLElement {
		controller: ModellyAppController | null = null;

		connectedCallback(): void {
			// At the time of connectedCallback, the child elements of the custom element are not yet parsed,
			// so we need to defer the initialization to the next frame.
			// Ref: https://stackoverflow.com/q/70949141/13103190
			window.requestAnimationFrame(() => {
				const modellyComponentOptions = this.parseModellyComponentOptions();
				const modellyLiteAppOptions = this.parseModellyLiteAppOptions();

				this.innerHTML = "";

				this.controller = create({
					target: this, // Same as `js/spa/src/main.ts`
					code: modellyLiteAppOptions.code,
					requirements: modellyLiteAppOptions.requirements,
					files: modellyLiteAppOptions.files,
					entrypoint: modellyLiteAppOptions.entrypoint,
					playground: this.hasAttribute("playground"),
					layout: this.getAttribute("layout"),
					...modellyComponentOptions
				});
			});
		}

		disconnectedCallback(): void {
			this.controller?.unmount();
		}

		parseModellyComponentOptions(): ModellyComponentOptions {
			// Parse the options from the attributes of the <modelly-lite> element.
			// The following attributes are supported:
			// * info: boolean
			// * container: boolean
			// * embed: boolean
			// * initial-height: string
			// * eager: boolean
			// * theme: "light" | "dark" | null
			// * auto-scroll: boolean
			// * control-page-title: boolean
			// * app-mode: boolean

			const info = this.hasAttribute("info");
			const container = this.hasAttribute("container");
			const isEmbed = this.hasAttribute("embed");
			const initialHeight = this.getAttribute("initial-height");
			const eager = this.hasAttribute("eager");
			const themeMode = this.getAttribute("theme");
			const autoScroll = this.hasAttribute("auto-scroll");
			const controlPageTitle = this.hasAttribute("control-page-title");
			const appMode = this.hasAttribute("app-mode");
			const sharedWorkerMode = this.hasAttribute("shared-worker");

			return {
				info,
				container,
				isEmbed,
				initialHeight: initialHeight ?? undefined,
				eager,
				themeMode:
					themeMode != null && ["light", "dark"].includes(themeMode)
						? (themeMode as ModellyComponentOptions["themeMode"])
						: null,
				autoScroll,
				controlPageTitle,
				appMode,
				sharedWorkerMode
			};
		}

		parseModellyLiteAppOptions(): ModellyLiteAppOptions {
			// When it contains child elements, parse them as options. Available child elements are:
			// * <modelly-file />
			//   Represents a file to be mounted in the virtual file system of the Wasm worker.
			//   At least 1 <modelly-file> element must have the `entrypoint` attribute.
			//   The following 2 forms are supported:
			//   * <modelly-file name="{file name}" >{file content}</modelly-file>
			//   * <modelly-file name="{file name}" url="{remote URL}" />
			// * <modelly-requirements>{requirements.txt}</modelly-requirements>
			// * <modelly-code>{Python code}</modelly-code>
			const options: ModellyLiteAppOptions = {};

			const fileElements = this.getElementsByTagName("modelly-file");
			for (const fileElement of fileElements) {
				const name = fileElement.getAttribute("name");
				if (name == null) {
					throw new Error("<modelly-file> must have the name attribute.");
				}

				const entrypoint = fileElement.hasAttribute("entrypoint");
				const url = fileElement.getAttribute("url");

				options.files ??= {};
				if (url != null) {
					options.files[name] = { url };
				} else {
					let data = fileElement.textContent ?? "";
					if (name.endsWith(".py")) {
						// Dedent the Python code.
						data = clean_indent(data);
					}
					options.files[name] = { data };
				}

				if (entrypoint) {
					if (options.entrypoint != null) {
						throw new Error("Multiple entrypoints are not allowed.");
					}
					options.entrypoint = name;
				}
			}

			if (options.entrypoint == null) {
				// If no entrypoint file is specified,
				// try to find the source code to be passed to the .code option instead.

				const codeElements = this.getElementsByTagName("modelly-code");
				if (codeElements.length === 0) {
					// If there is no <modelly-code> element, try to parse the content of the custom element as code.
					let code = "";
					this.childNodes.forEach((node) => {
						if (node.nodeType === Node.TEXT_NODE) {
							code += node.textContent;
						}
					});
					options.code = code || undefined;
				} else {
					if (codeElements.length > 1) {
						console.warn(
							"Multiple <modelly-code> elements are found. Only the first one will be used."
						);
					}
					const firstCodeElement = codeElements[0];
					options.code = firstCodeElement?.textContent ?? undefined;
				}
				options.code = options.code && clean_indent(options.code);
			}

			const requirementsElements = this.getElementsByTagName(
				"modelly-requirements"
			);
			if (requirementsElements.length > 1) {
				console.warn(
					"Multiple <modelly-requirements> elements are found. Only the first one will be used."
				);
			}
			const firstRequirementsElement = requirementsElements[0];
			const requirementsTxt = firstRequirementsElement?.textContent ?? "";
			options.requirements = parseRequirementsTxt(requirementsTxt);
			return options;
		}
	}

	customElements.define(CUSTOM_ELEMENT_NAME, ModellyLiteAppElement);
}
