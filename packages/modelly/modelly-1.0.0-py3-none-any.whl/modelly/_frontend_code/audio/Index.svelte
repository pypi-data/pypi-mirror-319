<svelte:options accessors={true} />

<script lang="ts">
	import type { Modelly, ShareData } from "@modelly/utils";

	import type { FileData } from "@modelly/client";
	import type { LoadingStatus } from "@modelly/statustracker";
	import { afterUpdate, onMount } from "svelte";

	import StaticAudio from "./static/StaticAudio.svelte";
	import InteractiveAudio from "./interactive/InteractiveAudio.svelte";
	import { StatusTracker } from "@modelly/statustracker";
	import { Block, UploadText } from "@modelly/atoms";
	import type { WaveformOptions } from "./shared/types";

	export let value_is_output = false;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let interactive: boolean;
	export let value: null | FileData = null;
	export let sources:
		| ["microphone"]
		| ["upload"]
		| ["microphone", "upload"]
		| ["upload", "microphone"];
	export let label: string;
	export let root: string;
	export let show_label: boolean;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let autoplay = false;
	export let loop = false;
	export let show_download_button: boolean;
	export let show_share_button = false;
	export let editable = true;
	export let waveform_options: WaveformOptions = {};
	export let pending: boolean;
	export let streaming: boolean;
	export let stream_every: number;
	export let input_ready: boolean;
	export let recording = false;
	let uploading = false;
	$: input_ready = !uploading;

	let stream_state = "closed";
	let _modify_stream: (state: "open" | "closed" | "waiting") => void;
	export function modify_stream_state(
		state: "open" | "closed" | "waiting"
	): void {
		stream_state = state;
		_modify_stream(state);
	}
	export const get_stream_state: () => void = () => stream_state;
	export let set_time_limit: (time: number) => void;
	export let modelly: Modelly<{
		input: never;
		change: typeof value;
		stream: typeof value;
		error: string;
		warning: string;
		edit: never;
		play: never;
		pause: never;
		stop: never;
		end: never;
		start_recording: never;
		pause_recording: never;
		stop_recording: never;
		upload: never;
		clear: never;
		share: ShareData;
		clear_status: LoadingStatus;
		close_stream: string;
	}>;

	let old_value: null | FileData = null;

	let active_source: "microphone" | "upload";

	let initial_value: null | FileData = value;

	$: if (value && initial_value === null) {
		initial_value = value;
	}

	const handle_reset_value = (): void => {
		if (initial_value === null || value === initial_value) {
			return;
		}

		value = initial_value;
	};

	$: {
		if (JSON.stringify(value) !== JSON.stringify(old_value)) {
			old_value = value;
			modelly.dispatch("change");
			if (!value_is_output) {
				modelly.dispatch("input");
			}
		}
	}

	let dragging: boolean;

	$: if (!active_source && sources) {
		active_source = sources[0];
	}

	let waveform_settings: Record<string, any>;

	let color_accent = "darkorange";

	onMount(() => {
		color_accent = getComputedStyle(document?.documentElement).getPropertyValue(
			"--color-accent"
		);
		set_trim_region_colour();
		waveform_settings.waveColor = waveform_options.waveform_color || "#9ca3af";
		waveform_settings.progressColor =
			waveform_options.waveform_progress_color || color_accent;
		waveform_settings.mediaControls = waveform_options.show_controls;
		waveform_settings.sampleRate = waveform_options.sample_rate || 44100;
	});

	$: waveform_settings = {
		height: 50,

		barWidth: 2,
		barGap: 3,
		cursorWidth: 2,
		cursorColor: "#ddd5e9",
		autoplay: autoplay,
		barRadius: 10,
		dragToSeek: true,
		normalize: true,
		minPxPerSec: 20
	};

	const trim_region_settings = {
		color: waveform_options.trim_region_color,
		drag: true,
		resize: true
	};

	function set_trim_region_colour(): void {
		document.documentElement.style.setProperty(
			"--trim-region-color",
			trim_region_settings.color || color_accent
		);
	}

	function handle_error({ detail }: CustomEvent<string>): void {
		const [level, status] = detail.includes("Invalid file type")
			? ["warning", "complete"]
			: ["error", "error"];
		loading_status = loading_status || {};
		loading_status.status = status as LoadingStatus["status"];
		loading_status.message = detail;
		modelly.dispatch(level as "error" | "warning", detail);
	}

	afterUpdate(() => {
		value_is_output = false;
	});
</script>

{#if !interactive}
	<Block
		variant={"solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		allow_overflow={false}
		{elem_id}
		{elem_classes}
		{visible}
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

		<StaticAudio
			i18n={modelly.i18n}
			{show_label}
			{show_download_button}
			{show_share_button}
			{value}
			{label}
			{loop}
			{waveform_settings}
			{waveform_options}
			{editable}
			on:share={(e) => modelly.dispatch("share", e.detail)}
			on:error={(e) => modelly.dispatch("error", e.detail)}
			on:play={() => modelly.dispatch("play")}
			on:pause={() => modelly.dispatch("pause")}
			on:stop={() => modelly.dispatch("stop")}
		/>
	</Block>
{:else}
	<Block
		variant={value === null && active_source === "upload" ? "dashed" : "solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		allow_overflow={false}
		{elem_id}
		{elem_classes}
		{visible}
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
		<InteractiveAudio
			{label}
			{show_label}
			{show_download_button}
			{value}
			on:change={({ detail }) => (value = detail)}
			on:stream={({ detail }) => {
				value = detail;
				modelly.dispatch("stream", value);
			}}
			on:drag={({ detail }) => (dragging = detail)}
			{root}
			{sources}
			{active_source}
			{pending}
			{streaming}
			bind:recording
			{loop}
			max_file_size={modelly.max_file_size}
			{handle_reset_value}
			{editable}
			bind:dragging
			bind:uploading
			on:edit={() => modelly.dispatch("edit")}
			on:play={() => modelly.dispatch("play")}
			on:pause={() => modelly.dispatch("pause")}
			on:stop={() => modelly.dispatch("stop")}
			on:start_recording={() => modelly.dispatch("start_recording")}
			on:pause_recording={() => modelly.dispatch("pause_recording")}
			on:stop_recording={(e) => modelly.dispatch("stop_recording")}
			on:upload={() => modelly.dispatch("upload")}
			on:clear={() => modelly.dispatch("clear")}
			on:error={handle_error}
			on:close_stream={() => modelly.dispatch("close_stream", "stream")}
			i18n={modelly.i18n}
			{waveform_settings}
			{waveform_options}
			{trim_region_settings}
			{stream_every}
			bind:modify_stream={_modify_stream}
			bind:set_time_limit
			upload={(...args) => modelly.client.upload(...args)}
			stream_handler={(...args) => modelly.client.stream(...args)}
		>
			<UploadText i18n={modelly.i18n} type="audio" />
		</InteractiveAudio>
	</Block>
{/if}
