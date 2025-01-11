<script context="module" lang="ts">
	export { default as BaseMarkdown } from "./shared/Markdown.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly, CopyData } from "@modelly/utils";
	import Markdown from "./shared/Markdown.svelte";

	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import { Block } from "@modelly/atoms";

	export let label: string;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let loading_status: LoadingStatus;
	export let rtl = false;
	export let sanitize_html = true;
	export let line_breaks = false;
	export let modelly: Modelly<{
		change: never;
		copy: CopyData;
		clear_status: LoadingStatus;
	}>;
	export let latex_delimiters: {
		left: string;
		right: string;
		display: boolean;
	}[];
	export let header_links = false;
	export let height: number | string | undefined;
	export let min_height: number | string | undefined;
	export let max_height: number | string | undefined;
	export let show_copy_button = false;
	export let container = false;

	$: label, modelly.dispatch("change");
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{container}
	allow_overflow={true}
	overflow_behavior="auto"
	{height}
	{min_height}
	{max_height}
>
	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		variant="center"
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>
	<div class:pending={loading_status?.status === "pending"}>
		<Markdown
			{value}
			{elem_classes}
			{visible}
			{rtl}
			on:change={() => modelly.dispatch("change")}
			on:copy={(e) => modelly.dispatch("copy", e.detail)}
			{latex_delimiters}
			{sanitize_html}
			{line_breaks}
			{header_links}
			{show_copy_button}
			root={modelly.root}
			{loading_status}
		/>
	</div>
</Block>

<style>
	div {
		transition: 150ms;
	}

	.pending {
		opacity: 0.2;
	}
</style>
