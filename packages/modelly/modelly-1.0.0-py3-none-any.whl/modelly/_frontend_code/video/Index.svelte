<svelte:options accessors={true} />

<script lang="ts">
	import type { Modelly, ShareData } from "@modelly/utils";

	import type { FileData } from "@modelly/client";
	import { Block, UploadText } from "@modelly/atoms";
	import StaticVideo from "./shared/VideoPreview.svelte";
	import Video from "./shared/InteractiveVideo.svelte";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: { video: FileData; subtitles: FileData | null } | null =
		null;
	let old_value: { video: FileData; subtitles: FileData | null } | null = null;

	export let label: string;
	export let sources:
		| ["webcam"]
		| ["upload"]
		| ["webcam", "upload"]
		| ["upload", "webcam"];
	export let root: string;
	export let show_label: boolean;
	export let loading_status: LoadingStatus;
	export let height: number | undefined;
	export let width: number | undefined;
	export let webcam_constraints: { [key: string]: any } | null = null;

	export let container = false;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let autoplay = false;
	export let show_share_button = true;
	export let show_download_button: boolean;
	export let modelly: Modelly<{
		change: never;
		clear: never;
		play: never;
		pause: never;
		upload: never;
		stop: never;
		end: never;
		start_recording: never;
		stop_recording: never;
		share: ShareData;
		error: string;
		warning: string;
		clear_status: LoadingStatus;
	}>;
	export let interactive: boolean;
	export let mirror_webcam: boolean;
	export let include_audio: boolean;
	export let loop = false;
	export let input_ready: boolean;
	let uploading = false;
	$: input_ready = !uploading;

	let _video: FileData | null = null;
	let _subtitle: FileData | null = null;

	let active_source: "webcam" | "upload";

	let initial_value: { video: FileData; subtitles: FileData | null } | null =
		value;

	$: if (value && initial_value === null) {
		initial_value = value;
	}

	const handle_reset_value = (): void => {
		if (initial_value === null || value === initial_value) {
			return;
		}

		value = initial_value;
	};

	$: if (sources && !active_source) {
		active_source = sources[0];
	}

	$: {
		if (value != null) {
			_video = value.video;
			_subtitle = value.subtitles;
		} else {
			_video = null;
			_subtitle = null;
		}
	}

	let dragging = false;

	$: {
		if (JSON.stringify(value) !== JSON.stringify(old_value)) {
			old_value = value;
			modelly.dispatch("change");
		}
	}

	function handle_change({ detail }: CustomEvent<FileData | null>): void {
		if (detail != null) {
			value = { video: detail, subtitles: null } as {
				video: FileData;
				subtitles: FileData | null;
			} | null;
		} else {
			value = null;
		}
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
</script>

{#if !interactive}
	<Block
		{visible}
		variant={value === null && active_source === "upload" ? "dashed" : "solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		{elem_id}
		{elem_classes}
		{height}
		{width}
		{container}
		{scale}
		{min_width}
		allow_overflow={false}
	>
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>

		<StaticVideo
			value={_video}
			subtitle={_subtitle}
			{label}
			{show_label}
			{autoplay}
			{loop}
			{show_share_button}
			{show_download_button}
			on:play={() => modelly.dispatch("play")}
			on:pause={() => modelly.dispatch("pause")}
			on:stop={() => modelly.dispatch("stop")}
			on:end={() => modelly.dispatch("end")}
			on:share={({ detail }) => modelly.dispatch("share", detail)}
			on:error={({ detail }) => modelly.dispatch("error", detail)}
			i18n={modelly.i18n}
			upload={(...args) => modelly.client.upload(...args)}
		/>
	</Block>
{:else}
	<Block
		{visible}
		variant={value === null && active_source === "upload" ? "dashed" : "solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		{elem_id}
		{elem_classes}
		{height}
		{width}
		{container}
		{scale}
		{min_width}
		allow_overflow={false}
	>
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>

		<Video
			value={_video}
			subtitle={_subtitle}
			on:change={handle_change}
			on:drag={({ detail }) => (dragging = detail)}
			on:error={handle_error}
			bind:uploading
			{label}
			{show_label}
			{show_download_button}
			{sources}
			{active_source}
			{mirror_webcam}
			{include_audio}
			{autoplay}
			{root}
			{loop}
			{webcam_constraints}
			{handle_reset_value}
			on:clear={() => modelly.dispatch("clear")}
			on:play={() => modelly.dispatch("play")}
			on:pause={() => modelly.dispatch("pause")}
			on:upload={() => modelly.dispatch("upload")}
			on:stop={() => modelly.dispatch("stop")}
			on:end={() => modelly.dispatch("end")}
			on:start_recording={() => modelly.dispatch("start_recording")}
			on:stop_recording={() => modelly.dispatch("stop_recording")}
			i18n={modelly.i18n}
			max_file_size={modelly.max_file_size}
			upload={(...args) => modelly.client.upload(...args)}
			stream_handler={(...args) => modelly.client.stream(...args)}
		>
			<UploadText i18n={modelly.i18n} type="video" />
		</Video>
	</Block>
{/if}
