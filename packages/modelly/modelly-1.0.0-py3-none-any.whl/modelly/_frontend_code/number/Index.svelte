<script lang="ts">
	import type { Modelly } from "@modelly/utils";
	import { Block, BlockTitle } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import { afterUpdate, tick } from "svelte";

	export let modelly: Modelly<{
		change: never;
		input: never;
		submit: never;
		blur: never;
		focus: never;
		clear_status: LoadingStatus;
	}>;
	export let label = modelly.i18n("number.number");
	export let info: string | undefined = undefined;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let value = 0;
	export let show_label: boolean;
	export let minimum: number | undefined = undefined;
	export let maximum: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let value_is_output = false;
	export let step: number | null = null;
	export let interactive: boolean;
	export let root: string;

	function handle_change(): void {
		if (!isNaN(value) && value !== null) {
			modelly.dispatch("change");
			if (!value_is_output) {
				modelly.dispatch("input");
			}
		}
	}
	afterUpdate(() => {
		value_is_output = false;
	});

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter") {
			e.preventDefault();
			modelly.dispatch("submit");
		}
	}

	$: value, handle_change();
	$: disabled = !interactive;
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
	<label class="block" class:container>
		<BlockTitle {root} {show_label} {info}>{label}</BlockTitle>
		<input
			aria-label={label}
			type="number"
			bind:value
			min={minimum}
			max={maximum}
			{step}
			on:keypress={handle_keypress}
			on:blur={() => modelly.dispatch("blur")}
			on:focus={() => modelly.dispatch("focus")}
			{disabled}
		/>
	</label>
</Block>

<style>
	label:not(.container),
	label:not(.container) > input {
		height: 100%;
		border: none;
	}
	.container > input {
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: var(--input-radius);
	}
	input[type="number"] {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
	}
	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
		background: var(--input-background-fill-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}

	input:out-of-range {
		border: var(--input-border-width) solid var(--error-border-color);
	}
</style>
