import { writable } from "svelte/store";

export interface Text {
  refId: string;
  content: string;
  createdAt: string;
}

export interface Image {
  refId?: string;
  url?: string;
  createdAt?: string;
}

export interface Generator {
  refId: string;
  text: Text;
  images?: Image[];
}

export interface GeneratorPreview {
  images?: Image[];
}

export const generator = writable<Generator>(null);
export const preview = writable<GeneratorPreview>(null);
