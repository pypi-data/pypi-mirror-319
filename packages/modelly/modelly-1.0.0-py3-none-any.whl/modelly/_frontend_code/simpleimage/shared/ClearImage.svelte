<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import { IconButton, IconButtonWrapper } from "@modelly/atoms";
	import { Clear } from "@modelly/icons";

	const dispatch = createEventDispatcher();
</script>

<IconButtonWrapper>
	<IconButton
		Icon={Clear}
		label="Remove Image"
		on:click={(event) => {
			dispatch("remove_image");
			event.stopPropagation();
		}}
	/>
</IconButtonWrapper>
