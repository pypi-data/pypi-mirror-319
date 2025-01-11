<script lang="ts">
	import type { Modelly } from "@modelly/utils";
	import HTML from "./shared/HTML.svelte";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import { Block, BlockLabel } from "@modelly/atoms";
	import { Code as CodeIcon } from "@modelly/icons";
	import { css_units } from "@modelly/utils";

	export let label = "HTML";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let loading_status: LoadingStatus;
	export let modelly: Modelly<{
		change: never;
		click: never;
		clear_status: LoadingStatus;
	}>;
	export let show_label = false;
	export let min_height: number | undefined = undefined;
	export let max_height: number | undefined = undefined;
	export let container = false;
	export let padding = true;

	$: label, modelly.dispatch("change");
</script>

<Block {visible} {elem_id} {elem_classes} {container} padding={false}>
	{#if show_label}
		<BlockLabel Icon={CodeIcon} {show_label} {label} float={false} />
	{/if}

	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
		variant="center"
		on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
	/>
	<div
		class="html-container"
		class:padding
		class:pending={loading_status?.status === "pending"}
		style:min-height={min_height && loading_status?.status !== "pending"
			? css_units(min_height)
			: undefined}
		style:max-height={max_height ? css_units(max_height) : undefined}
	>
		<HTML
			{value}
			{elem_classes}
			{visible}
			on:change={() => modelly.dispatch("change")}
			on:click={() => modelly.dispatch("click")}
		/>
	</div>
</Block>

<style>
	.padding {
		padding: var(--block-padding);
	}

	div {
		transition: 150ms;
	}

	.pending {
		opacity: 0.2;
	}
</style>
