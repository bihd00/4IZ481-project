<script lang="ts">
  import ModalDialog from "../ui/modal-dialog.svelte";
  import NavLinks from "./links.svelte";
</script>

<ModalDialog name={"nav"} title="Menu">
  <div class="flex flex-col gap-4 py-4">
    <NavLinks />
  </div>
</ModalDialog>
