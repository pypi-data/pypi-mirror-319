<svelte:options accessors={true} />

<script context="module" lang="ts">
	export { default as BaseMultimodalTextbox } from "./shared/MultimodalTextbox.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly, SelectData } from "@modelly/utils";
	import MultimodalTextbox from "./shared/MultimodalTextbox.svelte";
	import { Block } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import type { FileData } from "@modelly/client";
	import { onMount } from "svelte";
	import type { WaveformOptions } from "../audio/shared/types";

	export let modelly: Modelly<{
		change: typeof value;
		submit: never;
		stop: never;
		blur: never;
		select: SelectData;
		input: never;
		focus: never;
		error: string;
		clear_status: LoadingStatus;
		start_recording: never;
		pause_recording: never;
		stop_recording: never;
		upload: FileData[] | FileData;
		clear: undefined;
	}>;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: { text: string; files: FileData[] } = {
		text: "",
		files: []
	};
	export let file_types: string[] | null = null;
	export let lines: number;
	export let placeholder = "";
	export let label = "MultimodalTextbox";
	export let info: string | undefined = undefined;
	export let show_label: boolean;
	export let max_lines: number;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let submit_btn: string | boolean | null = null;
	export let stop_btn: string | boolean | null = null;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let rtl = false;
	export let text_align: "left" | "right" | undefined = undefined;
	export let autofocus = false;
	export let autoscroll = true;
	export let interactive: boolean;
	export let root: string;
	export let file_count: "single" | "multiple" | "directory";
	export let max_plain_text_length: number;
	export let sources: ["microphone" | "upload"] = ["upload"];
	export let waveform_options: WaveformOptions = {};

	let dragging: boolean;
	let active_source: "microphone" | null = null;
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
		autoplay: false,
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
</script>

<Block
	{visible}
	{elem_id}
	elem_classes={[...elem_classes, "multimodal-textbox"]}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={false}
	border_mode={dragging ? "focus" : "base"}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<MultimodalTextbox
		bind:value
		bind:value_is_output
		bind:dragging
		bind:active_source
		{file_types}
		{root}
		{label}
		{info}
		{show_label}
		{lines}
		{rtl}
		{text_align}
		{waveform_settings}
		i18n={modelly.i18n}
		max_lines={!max_lines ? lines + 1 : max_lines}
		{placeholder}
		{submit_btn}
		{stop_btn}
		{autofocus}
		{autoscroll}
		{file_count}
		{sources}
		max_file_size={modelly.max_file_size}
		on:change={() => modelly.dispatch("change", value)}
		on:input={() => modelly.dispatch("input")}
		on:submit={() => modelly.dispatch("submit")}
		on:stop={() => modelly.dispatch("stop")}
		on:blur={() => modelly.dispatch("blur")}
		on:select={(e) => modelly.dispatch("select", e.detail)}
		on:focus={() => modelly.dispatch("focus")}
		on:error={({ detail }) => {
			modelly.dispatch("error", detail);
		}}
		on:start_recording={() => modelly.dispatch("start_recording")}
		on:pause_recording={() => modelly.dispatch("pause_recording")}
		on:stop_recording={() => modelly.dispatch("stop_recording")}
		on:upload={(e) => modelly.dispatch("upload", e.detail)}
		on:clear={() => modelly.dispatch("clear")}
		disabled={!interactive}
		upload={(...args) => modelly.client.upload(...args)}
		stream_handler={(...args) => modelly.client.stream(...args)}
		{max_plain_text_length}
	/>
</Block>
