<script lang="ts">
  import { useNavigate } from "svelte-navigator";
  import { modal } from "../../stores/modal";
  import { user } from "../../stores/user";
  import Logo from "../../assets/logo.svg";
  import List from "../../assets/list.svg";
  import NavLinks from "./links.svelte";
  import Modal from "./modal.svelte";

  const navigate = useNavigate();
  $: $user == null ? navigate("/") : navigate("/dashboard");
</script>

<nav class="container mx-auto flex items-center justify-between pb-8">
  <h5 class="flex items-center">
    <img src={Logo} alt="Logo" class="w-12 md:w-auto" />
    <div class="ml-2 flex flex-col md:items-center">
      <span class="text-xl md:text-3xl font-bold uppercase">Cover</span>
      <span class="text-xs md:text-sm uppercase tracking-widest">Generator</span
      >
    </div>
  </h5>
  <div class="flex-row gap-4 hidden sm:flex">
    <NavLinks />
  </div>
  <div class="flex flex-col gap-4 sm:hidden block">
    <button on:click={() => modal.set("nav")} class="cursor-pointer">
      <img src={List} alt="List" class="w-12 md:w-auto" />
    </button>
  </div>
  <Modal />
</nav>
