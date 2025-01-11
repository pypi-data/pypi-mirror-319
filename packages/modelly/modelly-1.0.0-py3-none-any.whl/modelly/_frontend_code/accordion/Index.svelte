<script lang="ts">
	import Accordion from "./shared/Accordion.svelte";
	import { Block } from "@modelly/atoms";
	import { StatusTracker } from "@modelly/statustracker";
	import type { LoadingStatus } from "@modelly/statustracker";

	import Column from "@modelly/column";
	import type { Modelly } from "@modelly/utils";

	export let label: string;
	export let elem_id: string;
	export let elem_classes: string[];
	export let visible = true;
	export let open = true;
	export let loading_status: LoadingStatus;
	export let modelly: Modelly<{
		expand: never;
		collapse: never;
	}>;
</script>

<Block {elem_id} {elem_classes} {visible}>
	<StatusTracker
		autoscroll={modelly.autoscroll}
		i18n={modelly.i18n}
		{...loading_status}
	/>

	<Accordion
		{label}
		bind:open
		on:expand={() => modelly.dispatch("expand")}
		on:collapse={() => modelly.dispatch("collapse")}
	>
		<Column>
			<slot />
		</Column>
	</Accordion>
</Block>
