from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import ast
import operator as op

# 🔐 Your bot token (DO NOT share this)
import os
TOKEN = "7690049906:AAHN6eD_9bT_DK7KSe_NpOI4vlJj5CYXjck"

# Allowed math operators only
allowed_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)

    elif isinstance(node, ast.BinOp):
        return allowed_ops[type(node.op)](
            safe_eval(node.left),
            safe_eval(node.right)
        )

    elif isinstance(node, ast.UnaryOp):
        return allowed_ops[type(node.op)](
            safe_eval(node.operand)
        )

    elif isinstance(node, ast.Constant):
        return node.value

    else:
        raise ValueError("Invalid expression")


async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    try:
        tree = ast.parse(text, mode="eval")
        result = safe_eval(tree)

        # format result
        if isinstance(result, float):
            result = round(result, 2)
            if result.is_integer():
                result = int(result)

        await update.message.reply_text(f"{text} = {result}")

    except:
        await update.message.reply_text("❌ Only math allowed")


# Bot setup
app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculator))

print("Bot is running...")
app.run_polling()
