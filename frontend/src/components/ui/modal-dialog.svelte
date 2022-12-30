<script lang="ts">
  import { modal } from "../../stores/modal";
  export let name = "default";
  export let title = "";
  function closeModal() {
    modal.set(null);
  }
  function handleWindowKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      modal.set(null);
    }
  }
</script>

<svelte:window on:keydown={handleWindowKeyDown} />

<div
  on:click={closeModal}
  class="fixed top-0 left-0 w-full h-full overflow-x-hidden overflow-y-auto md:inset-0 md:h-full z-50 flex  
    {$modal === name ? '' : 'hidden'}"
  aria-hidden="true"
  tabindex="-1"
>
  <div
    class="w-full h-full absolute top-0 left-0 inset-0 z-20 bg-gray-900 bg-opacity-50 bg-opacity-80"
  />

  <div class="relative w-full max-w-lg md:h-auto mx-auto my-auto px-4 lg:px-0">
    <!-- Modal content -->
    <div
      on:click|stopPropagation
      aria-hidden="true"
      class="relative bg-white shadow bg-gray-700 z-40
      {$modal === name ? '' : 'hidden'}"
    >
      <!-- Modal header -->
      <div
        class="flex items-start justify-between p-4 border-b border-gray-600"
      >
        <h5 class="text-lg text-bold">{title}</h5>
        <button
          type="button"
          class="
            text-gray-400 
            bg-transparent 
            hover:bg-gray-200 
            hover:text-gray-900 
            rounded-lg 
            text-sm 
            p-1.5 
            ml-auto 
            inline-flex 
            items-center 
            hover:bg-gray-600 
            hover:text-white
            border border-solid border-slate-500"
          on:click={closeModal}
        >
          <svg
            aria-hidden="true"
            class="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
            ><path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            /></svg
          >
          <span class="sr-only">Close modal</span>
        </button>
      </div>
      <!-- Modal Body -->
      <div class="p-4">
        <slot />
      </div>
    </div>
  </div>
</div>
