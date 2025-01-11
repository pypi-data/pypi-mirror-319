<script context="module" lang="ts">
	export { default as BaseLabel } from "./shared/Label.svelte";
</script>

<script lang="ts">
	import type { Modelly, SelectData } from "@modelly/utils";
	import Label from "./shared/Label.svelte";
	import { LineChart as LabelIcon } from "@modelly/icons";
	import { Block, BlockLabel, Empty } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	export let modelly: Modelly<{
		change: never;
		select: SelectData;
		clear_status: LoadingStatus;
	}>;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let color: undefined | string = undefined;
	export let value: {
		label?: string;
		confidences?: { label: string; confidence: number }[];
	} = {};
	let old_value: typeof value | null = null;
	export let label = modelly.i18n("label.label");
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let show_label = true;
	export let _selectable = false;
	export let show_heading = true;

	$: {
		if (JSON.stringify(value) !== JSON.stringify(old_value)) {
			old_value = value;
			modelly.dispatch("change");
		}
	}

	$: _label = value.label;
</script>

<Block
	test_id="label"
	{visible}
	{elem_id}
	{elem_classes}
	{container}
	{scale}
	{min_width}
	padding={false}
>
	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>
	{#if show_label}
		<BlockLabel
			Icon={LabelIcon}
			{label}
			disable={container === false}
			float={show_heading === true}
		/>
	{/if}
	{#if _label !== undefined && _label !== null}
		<Label
			on:select={({ detail }) => modelly.dispatch("select", detail)}
			selectable={_selectable}
			{value}
			{color}
			{show_heading}
		/>
	{:else}
		<Empty unpadded_box={true}><LabelIcon /></Empty>
	{/if}
</Block>
