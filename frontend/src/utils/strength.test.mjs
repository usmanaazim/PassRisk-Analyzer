import { localStrengthHint } from "./demo.js";

const hint = localStrengthHint("abc");
if (hint.score <= 0) {
  throw new Error("local strength hint failed");
}
console.log("frontend util test ok");
