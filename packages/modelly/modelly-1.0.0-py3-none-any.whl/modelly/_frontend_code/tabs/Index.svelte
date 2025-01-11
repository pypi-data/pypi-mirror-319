<script context="module" lang="ts">
	export { default as BaseTabs, TABS, type Tab } from "./shared/Tabs.svelte";
</script>

<script lang="ts">
	import type { Modelly, SelectData } from "@modelly/utils";
	import { createEventDispatcher } from "svelte";
	import Tabs, { type Tab } from "./shared/Tabs.svelte";

	const dispatch = createEventDispatcher();

	export let visible = true;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let selected: number | string;
	export let initial_tabs: Tab[] = [];
	export let modelly:
		| Modelly<{
				change: never;
				select: SelectData;
		  }>
		| undefined;

	$: dispatch("prop_change", { selected });
</script>

<Tabs
	{visible}
	{elem_id}
	{elem_classes}
	bind:selected
	on:change={() => modelly?.dispatch("change")}
	on:select={(e) => modelly?.dispatch("select", e.detail)}
	{initial_tabs}
>
	<slot />
</Tabs>
