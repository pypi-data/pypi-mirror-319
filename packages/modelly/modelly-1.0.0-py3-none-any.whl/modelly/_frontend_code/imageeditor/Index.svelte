<svelte:options accessors={true} immutable={true} />

<script lang="ts">
	import type { Brush, Eraser } from "./shared/tools/Brush.svelte";
	import type {
		EditorData,
		ImageBlobs
	} from "./shared/InteractiveImageEditor.svelte";

	import type { Modelly, SelectData } from "@modelly/utils";
	import { BaseStaticImage as StaticImage } from "@modelly/image";
	import InteractiveImageEditor from "./shared/InteractiveImageEditor.svelte";
	import { Block } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import { tick } from "svelte";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: EditorData | null = {
		background: null,
		layers: [],
		composite: null
	};
	export let label: string;
	export let show_label: boolean;
	export let show_download_button: boolean;
	export let root: string;
	export let value_is_output = false;

	export let height: number | undefined = 450;
	export let width: number | undefined;

	export let _selectable = false;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let show_share_button = false;
	export let sources: ("clipboard" | "webcam" | "upload")[] = [
		"upload",
		"clipboard",
		"webcam"
	];
	export let interactive: boolean;
	export let placeholder: string | undefined;

	export let brush: Brush;
	export let eraser: Eraser;
	export let crop_size: [number, number] | `${string}:${string}` | null = null;
	export let transforms: "crop"[] = ["crop"];
	export let layers = true;
	export let attached_events: string[] = [];
	export let server: {
		accept_blobs: (a: any) => void;
	};
	export let canvas_size: [number, number] | undefined;
	export let show_fullscreen_button = true;
	export let full_history: any = null;

	export let modelly: Modelly<{
		change: never;
		error: string;
		input: never;
		edit: never;
		drag: never;
		apply: never;
		upload: never;
		clear: never;
		select: SelectData;
		share: ShareData;
		clear_status: LoadingStatus;
	}>;

	let editor_instance: InteractiveImageEditor;
	let image_id: null | string = null;

	export async function get_value(): Promise<ImageBlobs | { id: string }> {
		if (image_id) {
			const val = { id: image_id };
			image_id = null;
			return val;
		}

		const blobs = await editor_instance.get_data();

		return blobs;
	}

	let dragging: boolean;

	$: value && handle_change();
	const is_browser = typeof window !== "undefined";
	const raf = is_browser
		? window.requestAnimationFrame
		: (cb: (...args: any[]) => void) => cb();

	function wait_for_next_frame(): Promise<void> {
		return new Promise((resolve) => {
			raf(() => raf(() => resolve()));
		});
	}

	async function handle_change(): Promise<void> {
		await wait_for_next_frame();

		if (
			value &&
			(value.background || value.layers?.length || value.composite)
		) {
			modelly.dispatch("change");
		}
	}

	function handle_save(): void {
		modelly.dispatch("apply");
	}

	function handle_history_change(): void {
		modelly.dispatch("change");
		if (!value_is_output) {
			modelly.dispatch("input");
			tick().then((_) => (value_is_output = false));
		}
	}

	$: has_value = value?.background || value?.layers?.length || value?.composite;
</script>

{#if !interactive}
	<Block
		{visible}
		variant={"solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		{elem_id}
		{elem_classes}
		height={height || undefined}
		{width}
		allow_overflow={false}
		{container}
		{scale}
		{min_width}
	>
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>
		<StaticImage
			on:select={({ detail }) => modelly.dispatch("select", detail)}
			on:share={({ detail }) => modelly.dispatch("share", detail)}
			on:error={({ detail }) => modelly.dispatch("error", detail)}
			value={value?.composite || null}
			{label}
			{show_label}
			{show_download_button}
			selectable={_selectable}
			{show_share_button}
			i18n={modelly.i18n}
			{show_fullscreen_button}
		/>
	</Block>
{:else}
	<Block
		{visible}
		variant={has_value ? "solid" : "dashed"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		{elem_id}
		{elem_classes}
		height={height || undefined}
		{width}
		allow_overflow={false}
		{container}
		{scale}
		{min_width}
	>
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>

		<InteractiveImageEditor
			on:history={(e) => (full_history = e.detail)}
			bind:dragging
			{canvas_size}
			on:change={() => handle_history_change()}
			bind:image_id
			{crop_size}
			{value}
			bind:this={editor_instance}
			{root}
			{sources}
			{label}
			{show_label}
			{height}
			on:save={(e) => handle_save()}
			on:edit={() => modelly.dispatch("edit")}
			on:clear={() => modelly.dispatch("clear")}
			on:drag={({ detail }) => (dragging = detail)}
			on:upload={() => modelly.dispatch("upload")}
			on:share={({ detail }) => modelly.dispatch("share", detail)}
			on:error={({ detail }) => {
				loading_status = loading_status || {};
				loading_status.status = "error";
				modelly.dispatch("error", detail);
			}}
			on:error
			{brush}
			{eraser}
			changeable={attached_events.includes("apply")}
			realtime={attached_events.includes("change")}
			i18n={modelly.i18n}
			{transforms}
			accept_blobs={server.accept_blobs}
			{layers}
			status={loading_status?.status}
			upload={(...args) => modelly.client.upload(...args)}
			stream_handler={(...args) => modelly.client.stream(...args)}
			{placeholder}
			{full_history}
		></InteractiveImageEditor>
	</Block>
{/if}
