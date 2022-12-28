<!-- Is signed in  -->
<script lang="ts">
  import { user } from "../../stores/user";
</script>

{#if $user}
  <slot />
{:else}
  <slot name="signed-out" />
{/if}
