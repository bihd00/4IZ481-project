<script>
  import { modal } from "../../stores/modal";
  import { user } from "../../stores/user";
  import { signOut } from "../../services/firebase";

  function openSignIn() {
    modal.set("signin");
  }
</script>

<button
  on:click={$user ? signOut : openSignIn}
  class="border-solid border-2 border-sky-500 px-4 py-2"
  >{$user ? "Logout" : "Login"}</button
>
