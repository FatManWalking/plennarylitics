<script lang="ts">
import Nav from "$lib/daisy/navbar.svelte";
import { onMount } from "svelte";
import "../app.css";

import { isDark } from '../lib/stores/theme.store';
  
  const THEMES = {
      DARK: 'business',
      LIGHT: 'garden'
  };

  onMount(async () => {
    document.documentElement.setAttribute('data-theme', $isDark ? THEMES.DARK : THEMES.LIGHT);
    });

</script>

    <Nav/>
    <slot />
  