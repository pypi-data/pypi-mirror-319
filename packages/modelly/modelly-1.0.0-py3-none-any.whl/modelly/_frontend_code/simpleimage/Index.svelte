<svelte:options accessors={true} />

<script context="module" lang="ts">
	export { default as BaseImageUploader } from "./shared/ImageUploader.svelte";
	export { default as BaseStaticImage } from "./shared/ImagePreview.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly } from "@modelly/utils";
	import ImagePreview from "./shared/ImagePreview.svelte";
	import ImageUploader from "./shared/ImageUploader.svelte";

	import { Block, UploadText } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { FileData } from "@modelly/client";
	import type { LoadingStatus } from "@modelly/statustracker";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: null | FileData = null;
	export let label: string;
	export let show_label: boolean;
	export let show_download_button: boolean;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let interactive: boolean;
	export let root: string;
	export let placeholder: string | undefined = undefined;

	export let modelly: Modelly<{
		change: never;
		upload: never;
		clear: never;
		clear_status: LoadingStatus;
	}>;

	$: value, modelly.dispatch("change");

	let dragging: boolean;
</script>

{#if !interactive}
	<Block
		{visible}
		variant={"solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		{elem_id}
		{elem_classes}
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
		<ImagePreview
			{value}
			{label}
			{show_label}
			{show_download_button}
			i18n={modelly.i18n}
		/>
	</Block>
{:else}
	<Block
		{visible}
		variant={value === null ? "dashed" : "solid"}
		border_mode={dragging ? "focus" : "base"}
		padding={false}
		{elem_id}
		{elem_classes}
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

		<ImageUploader
			upload={(...args) => modelly.client.upload(...args)}
			stream_handler={(...args) => modelly.client.stream(...args)}
			bind:value
			{root}
			on:clear={() => modelly.dispatch("clear")}
			on:drag={({ detail }) => (dragging = detail)}
			on:upload={() => modelly.dispatch("upload")}
			{label}
			{show_label}
		>
			<UploadText i18n={modelly.i18n} type="image" {placeholder} />
		</ImageUploader>
	</Block>
{/if}
