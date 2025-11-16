const hre = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  const EquiExchange = await ethers.getContractFactory("EquiExchangeRecords");
  console.log("Deploying EquiExchangeRecords...");
  
  const equiExchange = await EquiExchange.deploy();
  await equiExchange.deployed(); // ✅ ethers v5 way

  console.log("\n✅ EquiExchangeRecords deployed to:", equiExchange.address);
  console.log("Network:", hre.network.name);
  
  // If on Sepolia, provide verification instructions
  if (hre.network.name === "sepolia") {
    console.log("\n📝 To verify on Etherscan, run:");
    console.log(`npx hardhat verify --network sepolia ${equiExchange.address}`);
    console.log("\n🔗 View on Etherscan:");
    console.log(`https://sepolia.etherscan.io/address/${equiExchange.address}`);
  }
  
  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    contractAddress: equiExchange.address,
    deployer: deployer.address,
    timestamp: new Date().toISOString()
  };
  
  console.log("\n📋 Deployment Info:");
  console.log(JSON.stringify(deploymentInfo, null, 2));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

