<script>
  import { Link, useLocation } from "svelte-navigator";
  import { modal } from "../../stores/modal";
  import { user } from "../../stores/user";
  import { signOut } from "../../services/firebase";
  import IfUser from "../users/if-user.svelte";

  const buttonClass = "px-4 py-2 text-left sm:border-solid sm:border-2";
  const activeClass = "bg-sky-500 sm:border-sky-200 sm:bg-inherit";
  const defaultClass = "bg-sky-800 sm:border-sky-500 sm:bg-inherit";
  const location = useLocation();
  $: activeHome = $location.pathname == "/";
  $: activeDashboard = $location.pathname == "/dashboard";

  function openSignIn() {
    modal.set("signin");
  }
</script>

<Link
  class="{buttonClass} {activeHome ? activeClass : defaultClass}"
  on:click={() => modal.set(null)}
  to="/">Home</Link
>
<IfUser>
  <Link
    class="{buttonClass} {activeDashboard ? activeClass : defaultClass}"
    on:click={() => modal.set(null)}
    to="/dashboard">Dashboard</Link
  >
</IfUser>

<button
  on:click={$user ? signOut : openSignIn}
  class="{buttonClass} {defaultClass}">{$user ? "Logout" : "Login"}</button
>
