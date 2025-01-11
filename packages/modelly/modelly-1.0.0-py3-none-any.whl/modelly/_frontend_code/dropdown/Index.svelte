<script context="module" lang="ts">
	export { default as BaseDropdown } from "./shared/Dropdown.svelte";
	export { default as BaseMultiselect } from "./shared/Multiselect.svelte";
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Modelly, KeyUpData, SelectData } from "@modelly/utils";
	import Multiselect from "./shared/Multiselect.svelte";
	import Dropdown from "./shared/Dropdown.svelte";
	import { Block } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	type Item = string | number;

	export let label = "Dropdown";
	export let info: string | undefined = undefined;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let multiselect = false;
	export let value: Item | Item[] | undefined = multiselect ? [] : undefined;
	export let value_is_output = false;
	export let max_choices: number | null = null;
	export let choices: [string, Item][];
	export let show_label: boolean;
	export let filterable: boolean;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let allow_custom_value = false;
	export let root: string;
	export let modelly: Modelly<{
		change: never;
		input: never;
		select: SelectData;
		blur: never;
		focus: never;
		key_up: KeyUpData;
		clear_status: LoadingStatus;
	}>;
	export let interactive: boolean;
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	padding={container}
	allow_overflow={false}
	{scale}
	{min_width}
>
	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>

	{#if multiselect}
		<Multiselect
			bind:value
			bind:value_is_output
			{choices}
			{max_choices}
			{root}
			{label}
			{info}
			{show_label}
			{allow_custom_value}
			{filterable}
			{container}
			i18n={modelly.i18n}
			on:change={() => modelly.dispatch("change")}
			on:input={() => modelly.dispatch("input")}
			on:select={(e) => modelly.dispatch("select", e.detail)}
			on:blur={() => modelly.dispatch("blur")}
			on:focus={() => modelly.dispatch("focus")}
			on:key_up={() => modelly.dispatch("key_up")}
			disabled={!interactive}
		/>
	{:else}
		<Dropdown
			bind:value
			bind:value_is_output
			{choices}
			{label}
			{root}
			{info}
			{show_label}
			{filterable}
			{allow_custom_value}
			{container}
			on:change={() => modelly.dispatch("change")}
			on:input={() => modelly.dispatch("input")}
			on:select={(e) => modelly.dispatch("select", e.detail)}
			on:blur={() => modelly.dispatch("blur")}
			on:focus={() => modelly.dispatch("focus")}
			on:key_up={(e) => modelly.dispatch("key_up", e.detail)}
			disabled={!interactive}
		/>
	{/if}
</Block>
