<script lang="ts">
	import type { Modelly } from "@modelly/utils";
	import { onDestroy } from "svelte";
	export let modelly: Modelly<{
		tick: never;
	}>;
	export let value = 1;
	export let active = true;
	let old_value: number;
	let old_active: boolean;
	let interval: NodeJS.Timeout;

	$: if (old_value !== value || active !== old_active) {
		if (interval) clearInterval(interval);
		if (active) {
			interval = setInterval(() => {
				if (document.visibilityState === "visible") modelly.dispatch("tick");
			}, value * 1000);
		}
		old_value = value;
		old_active = active;
	}

	onDestroy(() => {
		if (interval) clearInterval(interval);
	});
</script>
