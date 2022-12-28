<script lang="ts">
  import Nav from "./components/ui/nav.svelte";
  import ToastMessage from "./components/ui/toast-message.svelte";
  import SignIn from "./components/users/signin.svelte";
  import SigninButton from "./components/users/signin-button.svelte";
  import Generator from "./components/generator/generator.svelte";
  import Wrapper from "./components/ui/wrapper.svelte";
</script>

<main>
  <Wrapper>
    <Nav>
      <SigninButton />
    </Nav>
    <Generator />
    <ToastMessage />
    <SignIn />
  </Wrapper>
</main>
