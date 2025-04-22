import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "TIMEMINE" },
    { name: "description", content: "My Own Photo Library." },
  ];
}

export default function Home() {
  return <Welcome />;
}
