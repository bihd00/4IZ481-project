<script lang="ts">
  import IfUser from "../users/if-user.svelte";
  import { generator, type Generator } from "../../stores/generator";
  import { generateImages } from "../../services/firebase";
  import FileUploadButton from "../ui/file-upload-button.svelte";

  let currentGenerator: Generator;
  let textEl: HTMLTextAreaElement;
  let file: File;

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
    if (text == null || text.length < 10) return;
    const { serverError } = await generateImages(text);
    if (serverError) error = serverError;
    generator.subscribe((gen) => {
      currentGenerator = gen;
    });
  }

  async function handleUpload() {
    if (file == null || file.type !== "text/plain") return;
    const text = await file.text();
    textEl.value = text;
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
    class="container mx-auto mt-8 lg:h-[76vh] rounded-lg bg-zinc-900 p-4 flex flex-col items-stretch"
  >
    <h1 class="mb-4">Dashboard</h1>
    <div class="lg:grid lg:grid-cols-4 lg:gap-4 lg:grid-rows-1 lg:h-full">
      <!--  -->
      <div
        class="lg:pr-4 lg:border-r-2 lg:border-solid lg:border-zinc-800 mb-8 lg:mb-0"
      >
        <h2 class="text-2xl mb-2">Create</h2>
        <div class="mb-4">
          <FileUploadButton
            label="Upload a Text File"
            bind:file
            on:upload={handleUpload}
          />
        </div>
        <form on:submit|preventDefault={handleSubmit} class="flex flex-col">
          <label for="text" class="mb-2">Enter text manually</label>
          <textarea
            bind:this={textEl}
            name="text"
            id="text"
            rows="10"
            class="mb-3 bg-zinc-900 border-2 border-solid border-zinc-700 p-2"
          />
          <div class="">
            <button class="bg-sky-400 px-8 py-2 text-black font-bold"
              >{buttonText}
            </button>
          </div>
        </form>
      </div>
      <!--  -->
      <div class="lg:col-span-3">
        <h2 class="text-2xl mb-2">Results</h2>
        <div class="flex columns-auto gap-8 flex-wrap">
          {#if images.length}
            {#each images as img, i}
              <img
                id={`${img.refId}-img-${i}`}
                src={img.url}
                alt="Generated..."
              />
            {/each}
          {:else}
            <p class="text-gray-500">...no results yet 😐</p>
          {/if}
        </div>
      </div>
    </div>
  </section>
</IfUser>
