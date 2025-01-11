<script context="module" lang="ts">
	export { default as BaseCheckbox } from "./shared/Checkbox.svelte";
</script>

<script lang="ts">
	import type { Modelly } from "@modelly/utils";
	import { Block, Info } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import type { SelectData } from "@modelly/utils";
	import { afterUpdate } from "svelte";
	import BaseCheckbox from "./shared/Checkbox.svelte";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = false;
	export let value_is_output = false;
	export let label = "Checkbox";
	export let info: string | undefined = undefined;
	export let root: string;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let modelly: Modelly<{
		change: never;
		select: SelectData;
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let interactive: boolean;

	function handle_change(): void {
		modelly.dispatch("change");
		if (!value_is_output) {
			modelly.dispatch("input");
		}
	}
	afterUpdate(() => {
		value_is_output = false;
	});

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>

	{#if info}
		<Info {root} {info} />
	{/if}

	<BaseCheckbox
		bind:value
		{label}
		{interactive}
		on:change={handle_change}
		on:select={(e) => modelly.dispatch("select", e.detail)}
	/>
</Block>
