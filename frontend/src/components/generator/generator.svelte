<script lang="ts">
  import { userData } from "../../stores/user";
  import { generator, type Generator } from "../../stores/generator";
  import { generateImages } from "../../services/firebase";
  import FileUploadButton from "../ui/file-upload-button.svelte";
  import IfUser from "../users/if-user.svelte";

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
  $: previousImages = $userData?.images || [];
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
    class="container mx-auto mt-4 rounded-lg lg:bg-zinc-900 lg:p-4 lg:h-[80vh] flex flex-col items-stretch"
  >
    <h1 class="mb-4 text-3xl lg:text-4xl">Dashboard</h1>
    <div class="lg:grid lg:grid-cols-4 lg:gap-4 lg:grid-rows-2 lg:h-full">
      <!--  -->
      <div
        class="lg:pr-4 lg:border-r-2 lg:border-solid lg:border-zinc-800 mb-8 lg:mb-0 lg:row-span-2"
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
      <div class="mb-16 lg:mb-0 lg:col-span-3 lg:row-span-1">
        <h2 class="text-2xl mb-2">Results</h2>
        <div class="flex columns-auto gap-4 flex-wrap">
          {#if images.length}
            {#each images as img, i}
              <img
                id={`${img.refId}-img-${i}`}
                src={img.url}
                alt="Generated..."
              />
            {/each}
          {:else}
            <p class="text-gray-500">...</p>
          {/if}
        </div>
      </div>
      <!--  -->
      <div class="lg:col-span-3 lg:row-span-1">
        <h2 class="text-2xl mb-2">Previously Generated</h2>
        <div
          class="flex columns-auto gap-4 flex-nowrap max-w-full overflow-auto pb-4"
        >
          {#if previousImages.length}
            {#each previousImages as img, i}
              <img
                id={`${img.refId}-img-${i}`}
                src={img.url}
                alt="Generated..."
              />
            {/each}
          {:else}
            <p class="text-gray-500">...</p>
          {/if}
        </div>
      </div>
    </div>
  </section>
</IfUser>
