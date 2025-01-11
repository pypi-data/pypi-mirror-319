<script lang="ts">
	import { JsonView } from "@zerodevx/svelte-json-view";

	import type { Modelly } from "@modelly/utils";
	import { Block, Info } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";
	import type { SelectData } from "@modelly/utils";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = false;
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
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	{#if loading_status}
		<StatusTracker
			autoscroll={modelly.autoscroll}
			i18n={modelly.i18n}
			{...loading_status}
			on:clear_status={() => modelly.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<JsonView json={value} />
</Block>
