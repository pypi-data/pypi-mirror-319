<svelte:options accessors={true} />

<script context="module" lang="ts">
	export { default as BaseTextbox } from "./shared/Textbox.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly, SelectData, CopyData } from "@modelly/utils";
	import TextBox from "./shared/Textbox.svelte";
	import { Block } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	export let modelly: Modelly<{
		change: string;
		submit: never;
		blur: never;
		select: SelectData;
		input: never;
		focus: never;
		stop: never;
		clear_status: LoadingStatus;
		copy: CopyData;
	}>;
	export let label = "Textbox";
	export let info: string | undefined = undefined;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let lines: number;
	export let placeholder = "";
	export let show_label: boolean;
	export let max_lines: number;
	export let type: "text" | "password" | "email" = "text";
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let submit_btn: string | boolean | null = null;
	export let stop_btn: string | boolean | null = null;
	export let show_copy_button = false;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let rtl = false;
	export let text_align: "left" | "right" | undefined = undefined;
	export let autofocus = false;
	export let autoscroll = true;
	export let interactive: boolean;
	export let root: string;
	export let max_length: number | undefined = undefined;
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={container}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<TextBox
		bind:value
		bind:value_is_output
		{label}
		{info}
		{root}
		{show_label}
		{lines}
		{type}
		{rtl}
		{text_align}
		max_lines={!max_lines ? lines + 1 : max_lines}
		{placeholder}
		{submit_btn}
		{stop_btn}
		{show_copy_button}
		{autofocus}
		{container}
		{autoscroll}
		{max_length}
		on:change={() => modelly.dispatch("change", value)}
		on:input={() => modelly.dispatch("input")}
		on:submit={() => modelly.dispatch("submit")}
		on:blur={() => modelly.dispatch("blur")}
		on:select={(e) => modelly.dispatch("select", e.detail)}
		on:focus={() => modelly.dispatch("focus")}
		on:stop={() => modelly.dispatch("stop")}
		on:copy={(e) => modelly.dispatch("copy", e.detail)}
		disabled={!interactive}
	/>
</Block>
