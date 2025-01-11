<script lang="ts">
	import type { FileData } from "@modelly/client";
	import { BlockLabel, Empty } from "@modelly/atoms";
	import { File } from "@modelly/icons";
	import FilePreview from "./FilePreview.svelte";
	import type { I18nFormatter } from "@modelly/utils";

	export let value: FileData | FileData[] | null = null;
	export let label: string;
	export let show_label = true;
	export let selectable = false;
	export let height: number | undefined = undefined;
	export let i18n: I18nFormatter;
</script>

<BlockLabel
	{show_label}
	float={value === null}
	Icon={File}
	label={label || "File"}
/>

{#if value && (Array.isArray(value) ? value.length > 0 : true)}
	<FilePreview {i18n} {selectable} on:select on:download {value} {height} />
{:else}
	<Empty unpadded_box={true} size="large"><File /></Empty>
{/if}
