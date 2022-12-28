<script lang="ts">
  import { onMount } from "svelte";
  import { toast } from "../../stores/toast";
  let activate = false;
  let currentToast: any;
  let timeout: NodeJS.Timeout;
  let defaultIcons = {
    success: "✔️",
    error: "☠️",
    info: "💡",
  };
  let defaultColors = {
    success: "text-green-500",
    error: "text-red-500",
    info: "text-amber-400",
  };
  onMount(() => {
    toast.subscribe((msg) => {
      currentToast = msg;
      clearTimeout(timeout);
      if (msg) {
        timeout = setTimeout(() => {
          toast.set(null);
        }, msg?.delay || 10000);
        // delay hack for better animations
        activate = false;
        setTimeout(() => {
          activate = true;
        }, 200);
      }
    });
  });
  $: typeClass = currentToast?.type || "info";
</script>

{#if currentToast}
  <div class="fixed bottom-8 right-8">
    <div
      on:click={() => toast.set(null)}
      on:keydown
      role="alert"
      class="flex items-center p-4 space-x-4 w-full max-w-xs bg-white divide-x divide-gray-200 shadow 
        dark:divide-gray-700 space-x dark:bg-gray-900 cursor-pointer
        {defaultColors[typeClass] ?? 'text-gray-500'}
        {activate
        ? 'translate-x-0 visible opacity-100'
        : 'translate-x-100 invisible opacity-0'}"
    >
      {currentToast.icon ?? defaultIcons[currentToast.type ?? "info"]}
      <div class="pl-4 text-sm font-normal">
        {currentToast.message}
      </div>
    </div>
  </div>
{/if}
