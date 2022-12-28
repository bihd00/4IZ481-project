<script lang="ts">
  import { signInWithGoogle } from "../../services/firebase";
  import GoogleG from "../../assets/google-g.svg";
</script>

<button
  class="flex min-w-full justify-center gap-1 self-center items-center p-3 py-4 bg-slate-900 mb-2"
  on:click={signInWithGoogle}
>
  <img src={GoogleG} alt="Google G" />
  <span class="ml-1 font-bold">Sign in with Google</span>
</button>
