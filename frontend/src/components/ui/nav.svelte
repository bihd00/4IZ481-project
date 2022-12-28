<script lang="ts">
  import Logo from "../../assets/logo.svg";
</script>

<nav class="container mx-auto flex items-center justify-between pb-8">
  <h5 class="flex items-center">
    <img src={Logo} alt="Logo" class="w-12 md:w-auto" />
    <div class="ml-2 flex flex-col md:items-center">
      <span class="text-xl md:text-3xl font-bold uppercase">Cover</span>
      <span class="text-xs md:text-sm uppercase tracking-widest">Generator</span>
    </div>
  </h5>
  <div>
    <slot />
  </div>
</nav>
