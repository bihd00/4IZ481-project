<script>
  import { Link, useLocation } from "svelte-navigator";
  import { modal } from "../../stores/modal";
  import { user } from "../../stores/user";
  import { signOut } from "../../services/firebase";
  import IfUser from "../users/if-user.svelte";

  const buttonClass = "border-solid border-2 px-4 py-2 text-left";
  const location = useLocation();
  $: activeHome = $location.pathname == "/";
  $: activeDashboard = $location.pathname == "/dashboard";

  function openSignIn() {
    modal.set("signin");
  }
</script>

<Link
  class="{buttonClass} {activeHome ? 'border-sky-200' : 'border-sky-500'}"
  on:click={() => modal.set(null)}
  to="/">Home</Link
>
<IfUser>
  <Link
    class="{buttonClass} {activeDashboard
      ? 'border-sky-200'
      : 'border-sky-500'}"
    on:click={() => modal.set(null)}
    to="/dashboard">Dashboard</Link
  >
</IfUser>

<button
  on:click={$user ? signOut : openSignIn}
  class="{buttonClass} border-sky-500">{$user ? "Logout" : "Login"}</button
>
