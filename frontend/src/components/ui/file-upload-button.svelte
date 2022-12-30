<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import FileUpload from "../../assets/file-upload.svg";

  export let label = "Upload a File";
  export let file: File;
  let fileInput: HTMLInputElement;
  let filename: string;
  let isDragging = false;

  const dispatch = createEventDispatcher();
  function onDragenter() {
    isDragging = true;
  }
  function onDragLeave() {
    isDragging = false;
  }
  function setFile() {
    if (fileInput.files.length < 1) return;
    file = fileInput.files[0];
    if (file.name) {
      filename = file.name;
    }
    dispatch("upload");
  }
  $: isSet = file != null;
</script>

<label
  for="text-file"
  class="relative flex min-w-full justify-center gap-1 
         self-center items-center p-3 py-4 
         bg-zinc-900 lg:bg-zinc-800 mb-2 hover:bg-neutral-700
         {isDragging && !isSet ? 'border-2 border-dotted border-white' : ''}"
>
  <img src={FileUpload} alt="Upload a file..." />
  <span>{filename ? filename : label}</span>
  <input
    bind:this={fileInput}
    on:change={setFile}
    on:dragenter={onDragenter}
    on:dragleave={onDragLeave}
    class="cursor-pointer absolute top-0 
            left-0 w-full h-full opacity-0 d-block"
    id="text-file"
    type="file"
  />
</label>
