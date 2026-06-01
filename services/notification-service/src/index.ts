import express from "express";
import router from "./routes";
import { startConsumer } from "./consumer";

const PORT = process.env.PORT ?? 8004;

const app = express();
app.use(express.json());
app.use(router);
app.get("/v1/notifications", (req, res) => {
  res.json([
    {
      user_id: "test",
      message: "Notifications service is alive"
    }
  ]);
});

async function main(): Promise<void> {
  await startConsumer();
  app.listen(PORT, () => {
    console.log(`[notification-service] Running on http://localhost:${PORT}`);
  });
}

main().catch((err) => {
  console.error("[notification-service] Fatal error:", err);
  process.exit(1);
});
