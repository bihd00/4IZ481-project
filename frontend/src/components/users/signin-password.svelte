<script lang="ts">
  import {
    signInWithEmailAndPassword,
    signUpWithEmailAndPassword,
  } from "../../services/firebase";
  export let register = false;
  let emailEl: HTMLInputElement;
  let passwordEl: HTMLInputElement;
  let isValid = false;
  let isTouched = false;
  let loading = false;
  let confirmation: string;
  let error: string;
  function validate() {
    isValid = emailEl.validity.valid && passwordEl.validity.valid;
  }
  async function reset() {
    return await new Promise((resolve, _) => {
      setTimeout(() => {
        emailEl.value = "";
        passwordEl.value = "";
        confirmation = "";
        error = "";
        isValid = false;
        isTouched = false;
        loading = false;
        resolve(true);
      }, 2500);
    });
  }
  async function handleSubmit(_) {
    let submitFn = register
      ? signUpWithEmailAndPassword
      : signInWithEmailAndPassword;
    const email = emailEl.value.toLowerCase();
    const password = passwordEl.value;
    loading = true;
    const { res, serverError } = await submitFn(email, password);
    loading = false;
    error = serverError;
    confirmation = res;
    await reset();
  }
</script>

<form
  on:submit|preventDefault={handleSubmit}
  class="flex flex-col min-w-full gap-2"
>
  <label for="email">Email</label>
  <input
    class="p-1 h-10"
    type="email"
    name="email"
    bind:this={emailEl}
    on:input={validate}
    on:focus|once={() => (isTouched = true)}
    class:touched={isTouched}
    required
  />
  <label for="email">Password</label>
  <input
    class="p-1 h-10"
    type="password"
    name="password"
    bind:this={passwordEl}
    on:input={validate}
    on:focus|once={() => (isTouched = true)}
    class:touched={isTouched}
    required
  />
  {#if error}
    <p class="text-red-400">{error}</p>
  {/if}
  {#if confirmation}
    <p class="text-green-400">{confirmation}</p>
  {/if}

  <div class="mt-2">
    <button
      class="p-2 px-6 border-slate-500 border-2 border-solid"
      type="submit"
      class:disabled={!isValid || loading}
    >
      {loading ? "sending..." : "send"}
    </button>
  </div>
</form>
