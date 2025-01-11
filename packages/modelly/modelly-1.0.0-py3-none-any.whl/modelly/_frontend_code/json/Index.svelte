<script lang="ts" context="module">
	export { default as BaseJSON } from "./shared/JSON.svelte";
</script>

<script lang="ts">
	import type { Modelly } from "@modelly/utils";
	import JSON from "./shared/JSON.svelte";
	import { Block, BlockLabel } from "@modelly/atoms";
	import { JSON as JSONIcon } from "@modelly/icons";

	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: any;
	let old_value: any;
	export let loading_status: LoadingStatus;
	export let label: string;
	export let show_label: boolean;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let modelly: Modelly<{
		change: never;
		clear_status: LoadingStatus;
	}>;
	export let open = false;
	export let theme_mode: "system" | "light" | "dark";
	export let show_indices: boolean;
	export let height: number | string | undefined;
	export let min_height: number | string | undefined;
	export let max_height: number | string | undefined;

	$: {
		if (value !== old_value) {
			old_value = value;
			modelly.dispatch("change");
		}
	}

	let label_height = 0;
</script>

<Block
	{visible}
	test_id="json"
	{elem_id}
	{elem_classes}
	{container}
	{scale}
	{min_width}
	padding={false}
	allow_overflow={true}
	overflow_behavior="auto"
	{height}
	{min_height}
	{max_height}
>
	<div bind:clientHeight={label_height}>
		{#if label}
			<BlockLabel
				Icon={JSONIcon}
				{show_label}
				{label}
				float={false}
				disable={container === false}
			/>
		{/if}
	</div>

	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>

	<JSON {value} {open} {theme_mode} {show_indices} {label_height} />
</Block>
