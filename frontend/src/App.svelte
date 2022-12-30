<script lang="ts">
  import { Router, Route } from "svelte-navigator";
  import Nav from "./components/nav/nav.svelte";
  import ToastMessage from "./components/ui/toast-message.svelte";
  import SignIn from "./components/users/signin.svelte";
  import Generator from "./pages/generator.svelte";
  import Home from "./pages/home.svelte";
  import Wrapper from "./components/ui/wrapper.svelte";
</script>

<Router>
  <main>
    <Wrapper>
      <Nav />
      <div>
        <Route path="/" primary={false}>
          <Home />
        </Route>
        <Route path="/dashboard" primary={false}>
          <Generator />
        </Route>
      </div>
      <ToastMessage />
      <SignIn />
    </Wrapper>
  </main>
</Router>
