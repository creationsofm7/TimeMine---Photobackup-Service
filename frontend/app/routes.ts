import { type RouteConfig, route, index } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("upload", "routes/Uploader.tsx"),
] satisfies RouteConfig;
