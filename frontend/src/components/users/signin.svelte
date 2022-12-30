<script lang="ts">
  import SigninPassword from "./signin-password.svelte";
  import SigninGoogle from "./signin-google.svelte";
  import ModalDialog from "../ui/modal-dialog.svelte";
  import { modal } from "../../stores/modal";

  let modalTitle: string;
  $: isRegistering = $modal == null;

  function toggleTitle() {
    modalTitle = isRegistering ? "Register" : "Login";
  }

  function toggleRegister() {
    isRegistering = !isRegistering;
    toggleTitle();
  }


  toggleTitle();
</script>

<ModalDialog name={"signin"} title={modalTitle}>
  <SigninPassword register={isRegistering} />
  {#if !isRegistering}
    <p class="mt-8" />
    <SigninGoogle />
    <button
      class="flex min-w-full justify-center gap-1 self-center items-center p-3 py-4 bg-slate-800 mb-2"
      on:click={toggleRegister}
      >Register
    </button>
  {:else}
    <button
      class="mt-10 flex min-w-full justify-center gap-1 self-center items-center p-3 py-4 bg-slate-800 mb-2"
      on:click={toggleRegister}
      >Back to Login
    </button>
  {/if}
</ModalDialog>
