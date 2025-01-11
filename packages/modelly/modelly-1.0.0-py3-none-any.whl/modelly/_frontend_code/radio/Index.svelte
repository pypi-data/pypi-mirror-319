<script context="module" lang="ts">
	export { default as BaseRadio } from "./shared/Radio.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly, SelectData } from "@modelly/utils";
	import { afterUpdate } from "svelte";
	import { Block, BlockTitle } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import BaseRadio from "./shared/Radio.svelte";

	export let modelly: Modelly<{
		change: never;
		select: SelectData;
		input: never;
		clear_status: LoadingStatus;
	}>;

	export let label = modelly.i18n("radio.radio");
	export let info: string | undefined = undefined;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: string | null = null;
	export let choices: [string, string | number][] = [];
	export let show_label = true;
	export let container = false;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let interactive = true;
	export let root: string;

	function handle_change(): void {
		modelly.dispatch("change");
	}

	let old_value = value;
	$: {
		if (value !== old_value) {
			old_value = value;
			handle_change();
		}
	}
	$: disabled = !interactive;
</script>

<Block
	{visible}
	type="fieldset"
	{elem_id}
	{elem_classes}
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

	<BlockTitle {root} {show_label} {info}>{label}</BlockTitle>

	<div class="wrap">
		{#each choices as [display_value, internal_value], i (i)}
			<BaseRadio
				{display_value}
				{internal_value}
				bind:selected={value}
				{disabled}
				on:input={() => {
					modelly.dispatch("select", { value: internal_value, index: i });
					modelly.dispatch("input");
				}}
			/>
		{/each}
	</div>
</Block>

<style>
	.wrap {
		display: flex;
		flex-wrap: wrap;
		gap: var(--checkbox-label-gap);
	}
</style>
