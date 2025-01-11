<svelte:options accessors={true} />

<script context="module" lang="ts">
	export { default as FilePreview } from "./shared/FilePreview.svelte";
	export { default as BaseFileUpload } from "./shared/FileUpload.svelte";
	export { default as BaseFile } from "./shared/File.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly, SelectData } from "@modelly/utils";
	import File from "./shared/File.svelte";
	import FileUpload from "./shared/FileUpload.svelte";
	import type { FileData } from "@modelly/client";
	import { Block, UploadText } from "@modelly/atoms";

	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: null | FileData | FileData[];

	export let interactive: boolean;
	export let root: string;
	export let label: string;
	export let show_label: boolean;
	export let height: number | undefined = undefined;

	export let _selectable = false;
	export let loading_status: LoadingStatus;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let modelly: Modelly<{
		change: never;
		error: string;
		upload: never;
		clear: never;
		select: SelectData;
		clear_status: LoadingStatus;
		delete: FileData;
		download: FileData;
	}>;
	export let file_count: "single" | "multiple" | "directory";
	export let file_types: string[] = ["file"];
	export let input_ready: boolean;
	export let allow_reordering = false;
	let uploading = false;
	$: input_ready = !uploading;

	let old_value = value;
	$: if (JSON.stringify(old_value) !== JSON.stringify(value)) {
		modelly.dispatch("change");
		old_value = value;
	}

	let dragging = false;
	let pending_upload = false;
</script>

<Block
	{visible}
	variant={value ? "solid" : "dashed"}
	border_mode={dragging ? "focus" : "base"}
	padding={false}
	{elem_id}
	{elem_classes}
	{container}
	{scale}
	{min_width}
	allow_overflow={false}
>
	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		status={pending_upload
			? "generating"
			: loading_status?.status || "complete"}
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>
	{#if !interactive}
		<File
			on:select={({ detail }) => modelly.dispatch("select", detail)}
			on:download={({ detail }) => modelly.dispatch("download", detail)}
			selectable={_selectable}
			{value}
			{label}
			{show_label}
			{height}
			i18n={modelly.i18n}
		/>
	{:else}
		<FileUpload
			upload={(...args) => modelly.client.upload(...args)}
			stream_handler={(...args) => modelly.client.stream(...args)}
			{label}
			{show_label}
			{value}
			{file_count}
			{file_types}
			selectable={_selectable}
			{root}
			{height}
			{allow_reordering}
			bind:uploading
			max_file_size={modelly.max_file_size}
			on:change={({ detail }) => {
				value = detail;
			}}
			on:drag={({ detail }) => (dragging = detail)}
			on:clear={() => modelly.dispatch("clear")}
			on:select={({ detail }) => modelly.dispatch("select", detail)}
			on:upload={() => modelly.dispatch("upload")}
			on:error={({ detail }) => {
				loading_status = loading_status || {};
				loading_status.status = "error";
				modelly.dispatch("error", detail);
			}}
			on:delete={({ detail }) => {
				modelly.dispatch("delete", detail);
			}}
			i18n={modelly.i18n}
		>
			<UploadText i18n={modelly.i18n} type="file" />
		</FileUpload>
	{/if}
</Block>
