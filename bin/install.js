#!/usr/bin/env node
const { run, detectPython, detectPip, detectPipx, isSuperClaudeInstalled, isSuperClaudeInstalledPipx, checkPythonEnvironment } = require("./checkEnv");

console.log("🔍 環境を確認中...");

let pythonCmd = detectPython();
if (!pythonCmd) {
  console.error("❌ Python 3が必要ですが、見つかりません。");
  console.error("   https://python.org からPython 3.8以降をインストールしてください");
  process.exit(1);
}
console.log(`✅ Pythonが見つかりました: ${pythonCmd}`);

// Check if we're in an externally managed environment (PEP 668)
const isExternallyManaged = checkPythonEnvironment();
let installMethod = null;
let isInstalled = false;

if (isExternallyManaged) {
  console.log("📦 外部で管理されているPython環境（PEP 668）を検出しました");
  
  // Try pipx first for externally managed environments
  let pipxCmd = detectPipx();
  if (pipxCmd) {
    console.log(`✅ pipxが見つかりました: ${pipxCmd}`);
    installMethod = "pipx";
    isInstalled = isSuperClaudeInstalledPipx();
  } else {
    console.log("⚠️ このシステムではpipxが推奨されますが、見つかりません。");
    console.log("   pipxは次のコマンドでインストールできます: apt install pipx (Ubuntu/Debian) または brew install pipx (macOS)");
    console.log("   または、次のいずれかを使用してください:");
    console.log("     pip install --user SuperClaude  # 推奨");
    console.log("     pip install --break-system-packages SuperClaude  # 強制 (注意して使用)");
    
    // Fall back to pip with --user flag
    let pipCmd = detectPip();
    if (pipCmd) {
      console.log(`✅ pipが見つかりました: ${pipCmd}`);
      console.log("   --userフラグを使用してインストールを試みます");
      installMethod = "pip-user";
      isInstalled = isSuperClaudeInstalled(pipCmd);
    } else {
      console.error("❌ pipxもpipも見つかりません。いずれかをインストールしてください。");
      process.exit(1);
    }
  }
} else {
  // Standard environment - use pip normally
  let pipCmd = detectPip();
  if (!pipCmd) {
    console.error("❌ pipが必要ですが、見つかりません。");
    console.error("   pipをインストールするか、システムのパッケージマネージャを使用してください");
    process.exit(1);
  }
  console.log(`✅ pipが見つかりました: ${pipCmd}`);
  installMethod = "pip";
  isInstalled = isSuperClaudeInstalled(pipCmd);
}

// Perform installation based on detected method
if (!isInstalled) {
  console.log("📦 PyPIからSuperClaudeをインストール中...");
  
  let result;
  switch(installMethod) {
    case "pipx":
      result = run("pipx", ["install", "SuperClaude"], { stdio: "inherit" });
      break;
    case "pip-user":
      result = run(detectPip(), ["install", "--user", "SuperClaude"], { stdio: "inherit" });
      break;
    case "pip":
      result = run(detectPip(), ["install", "SuperClaude"], { stdio: "inherit" });
      break;
  }
  
  if (result.status !== 0) {
    console.error("❌ インストールに失敗しました。");
    if (installMethod === "pip" && isExternallyManaged) {
      console.error("   お使いのシステムでは、pipインストールにpipxまたは--userフラグが必要です。");
      console.error("   試行: pipx install SuperClaude");
      console.error("   または:  pip install --user SuperClaude");
    }
    process.exit(1);
  }
  console.log("✅ SuperClaudeが正常にインストールされました！");
  
  // For pipx installations, ensure it's in PATH
  if (installMethod === "pipx") {
    console.log("\n📌 注意: 'SuperClaude'コマンドが見つからない場合は、次を実行してください:");
    console.log("   pipx ensurepath");
    console.log("   その後、ターミナルを再起動するか、次を実行してください: source ~/.bashrc");
  }
} else {
  console.log("✅ SuperClaudeは既にインストールされています。");
}

// Try to run SuperClaude install
console.log("\n🚀 SuperClaudeのインストールを実行中...");
const installResult = run("SuperClaude", ["install"], { stdio: "inherit" });

if (installResult.status !== 0) {
  console.log("\n⚠️ 'SuperClaude install'を自動的に実行できませんでした。");
  console.log("   SuperClaudeがPATHに含まれていることを確認した後、手動で実行してください:");
  console.log("   SuperClaude install");
  
  if (installMethod === "pipx") {
    console.log("\n   コマンドが見つからない場合は、次を試してください:");
    console.log("   pipx ensurepath && source ~/.bashrc");
  } else if (installMethod === "pip-user") {
    console.log("\n   コマンドが見つからない場合は、PythonのユーザーbinをPATHに追加してください:");
    console.log("   export PATH=\"$HOME/.local/bin:$PATH\"");
  }
}