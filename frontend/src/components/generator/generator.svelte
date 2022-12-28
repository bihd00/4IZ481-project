<script lang="ts">
  import IfUser from "../users/if-user.svelte";
  import { generator, type Generator } from "../../stores/generator";
  import { generateImages } from "../../services/firebase";

  let currentGenerator: Generator;
  let textEl: HTMLTextAreaElement;
  let confirmation: string;
  let loading = false;
  let error: string;

  function reset() {
    if (!currentGenerator) return;
    if (!currentGenerator.images) return;
    if (currentGenerator.images.length < 1) return;
    loading = false;
    error = null;
    confirmation = "Done!";
    setTimeout(() => {
      confirmation = null;
    }, 3000);
  }

  async function handleSubmit() {
    loading = true;
    const text = textEl.value;
    const { serverError } = await generateImages(text);
    if (serverError) error = serverError;
    generator.subscribe((gen) => {
      currentGenerator = gen;
    });
  }
  $: images = currentGenerator?.images || [];
  $: $generator, reset();
  $: buttonText = confirmation
    ? confirmation
    : loading
    ? "Working on it..."
    : error
    ? error
    : "Generate";
</script>

<IfUser>
  <section
    class="container mx-auto mt-8 flex flex-col items-center justify-center h-[76vh]"
  >
    <div class="h-full w-full sm:h-2/3 sm:w-2/3 sm:mb-24 xl:w-1/2">
      <form
        on:submit|preventDefault={handleSubmit}
        class="flex flex-col gap-4 h-full"
      >
        <label for="text">Enter your cover text</label>
        <textarea bind:this={textEl} name="text" id="text" class="h-full" />
        <div class="">
          <button
            class="border-solid border-2 border-white px-8 py-2"
            type="submit"
            >{buttonText}
          </button>
        </div>
      </form>
    </div>
  </section>
  {#if images}
    <section class="container mx-auto mt-8 flex">
      {#each images as img, i}
        <img id={`${img.refId}-img-${i}`} src={img.url} alt="Generated..." />
      {/each}
    </section>
  {/if}
</IfUser>
