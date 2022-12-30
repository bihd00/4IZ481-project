<script lang="ts">
  import { preview } from "../stores/generator";
  import { onMount } from "svelte";
  import { getPreviewImages } from "../services/firebase";

  onMount(async () => {
    await getPreviewImages();
  });

  $: images = $preview?.images || [];
</script>

<div class="container mx-auto h-full mt-4">
  <h1 class="text-3xl xs:text-4xl">Recently Generated</h1>

  <div class="mt-8 gap-4 xs:gap-8 columns-2 md:columns-3 lg:columns-5">
    {#if images}
      {#each images as img, i}
        <img
          id={`${img.refId}-img-${i}`}
          src={img.url}
          class="w-full aspect-square mb-4 xs:mb-8 drop-shadow-2xl {i == 9
            ? 'md:hidden lg:block'
            : ''}"
          alt="Generated..."
        />
      {/each}
    {/if}
  </div>
</div>
