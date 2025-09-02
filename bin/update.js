#!/usr/bin/env node
const { run, detectPip, detectPipx, isSuperClaudeInstalledPipx, checkPythonEnvironment } = require("./checkEnv");

console.log("🔄 SuperClaudeの更新を確認中...");

// Detect installation method
const isExternallyManaged = checkPythonEnvironment();
let updateMethod = null;

// Check if installed via pipx
if (detectPipx() && isSuperClaudeInstalledPipx()) {
  updateMethod = "pipx";
  console.log("✅ pipxインストールを検出しました");
} else {
  // Check for pip installation
  let pipCmd = detectPip();
  if (!pipCmd) {
    console.error("❌ pipxもpipも見つかりません、更新できません。");
    console.error("   最初にSuperClaudeをインストールしてください:");
    console.error("   pipx install SuperClaude");
    console.error("   または");
    console.error("   pip install SuperClaude");
    process.exit(1);
  }
  
  if (isExternallyManaged) {
    updateMethod = "pip-user";
    console.log("✅ --userフラグ付きのpipインストールを検出しました");
  } else {
    updateMethod = "pip";
    console.log("✅ 標準のpipインストールを検出しました");
  }
}

// Perform update based on detected method
console.log("🔄 PyPIからSuperClaudeを更新中...");

let result;
switch(updateMethod) {
  case "pipx":
    result = run("pipx", ["upgrade", "SuperClaude"], { stdio: "inherit" });
    break;
  case "pip-user":
    result = run(detectPip(), ["install", "--upgrade", "--user", "SuperClaude"], { stdio: "inherit" });
    break;
  case "pip":
    result = run(detectPip(), ["install", "--upgrade", "SuperClaude"], { stdio: "inherit" });
    break;
}

if (result.status !== 0) {
  console.error("❌ 更新に失敗しました。");
  if (updateMethod === "pip" && isExternallyManaged) {
    console.error("   お使いのシステムでは、pip操作にpipxまたは--userフラグが必要です。");
    console.error("   試してみてください: pipx upgrade SuperClaude");
    console.error("   または:  pip install --upgrade --user SuperClaude");
  }
  process.exit(1);
}

console.log("✅ SuperClaudeは正常に更新されました！");

// Run SuperClaude update command
console.log("\n🚀 Running SuperClaude update...");
const updateResult = run("SuperClaude", ["update"], { stdio: "inherit" });

if (updateResult.status !== 0) {
  console.log("\n⚠️  Could not run 'SuperClaude update' automatically.");
  console.log("   手動で実行してください:");
  console.log("   SuperClaude update");
}