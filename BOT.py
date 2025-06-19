import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from AI_LOCAL import resposta_simples
from AI_LLM import resposta_deepseek
from dotenv import load_dotenv
load_dotenv()

load_dotenv()
print("🔐 Chave LLM carregada:", os.getenv("DEEPSEEK_API_KEY"))
TOKEN = os.getenv("DISCORD_TOKEN")
USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Verifica se está no canal certo
def canal_lumora(ctx):
    return ctx.channel.name == "lumorabot"

def apenas_canal_lumora():
    def predicado(ctx):
        return canal_lumora(ctx)
    return commands.check(predicado)

@bot.command(name="UsoAvançado")
@apenas_canal_lumora()
async def uso_avancado(ctx, *, pergunta):
    if USE_LLM:
        resposta = resposta_deepseek(pergunta)
        await ctx.send(resposta)
    else:
        await ctx.send("LLM desativada. Ative no arquivo .env")

@bot.command(name="UsoSimples")
@apenas_canal_lumora()
async def uso_simples(ctx, *, pergunta):
    resposta = resposta_simples(pergunta)
    await ctx.send(resposta)

@bot.event
async def on_ready():
    print(f"🤖 {bot.user} está online!")

    guild = bot.guilds[0]
    canal = discord.utils.get(guild.text_channels, name="lumorabot")
    if canal:
        mensagem_fixa = (
            "🛑 **Aviso Importante:**\n"
            "Use os comandos do bot apenas neste canal.\n"
            "Para dúvidas, fale com a equipe Lumora Sync."
        )
        fixadas = await canal.pins()
        if not any(m.content == mensagem_fixa for m in fixadas):
            msg = await canal.send(mensagem_fixa)
            await msg.pin()
            print("Mensagem fixa enviada e fixada.")
        else:
            print("Mensagem fixa já existe no canal.")
    else:
        print("Canal lumorabot não encontrado.")

@bot.event
async def on_member_join(member):
    canal_entrada = discord.utils.get(member.guild.text_channels, name='entrada')
    if canal_entrada:
        await canal_entrada.send(
            f"🎉 Seja bem-vindo(a), {member.mention} à **Lumora Sync**!\n"
            f"Aproveite o servidor e pergunte sobre nossos projetos 💡"
        )

@bot.event
async def on_member_remove(member):
    canal_saida = discord.utils.get(member.guild.text_channels, name='saída')
    if canal_saida:
        await canal_saida.send(
            f"😢 {member.name} saiu do servidor. Até mais!"
        )

@bot.command()
@apenas_canal_lumora()
async def oi(ctx):
    await ctx.send("Olá! Eu sou o Lumora Sync Bot 🤖")

@bot.command()
@apenas_canal_lumora()
async def local(ctx, *, pergunta):
    resposta = resposta_simples(pergunta)
    await ctx.send(resposta)

@bot.command()
@apenas_canal_lumora()
async def smart(ctx, *, pergunta):
    if USE_LLM:
        resposta = resposta_deepseek(pergunta)
        await ctx.send(resposta)
    else:
        await ctx.send("LLM desativada. Ative no arquivo .env")

@bot.command()
@commands.has_permissions(manage_roles=True)
@apenas_canal_lumora()
async def cargo(ctx, membro: discord.Member, *, nome_do_cargo):
    cargo_autorizado = discord.utils.get(ctx.guild.roles, name="Administrador")
    dono_id = 123456789012345678  # Substitua com seu ID

    if ctx.author.id != dono_id and (not cargo_autorizado or cargo_autorizado not in ctx.author.roles):
        await ctx.send("❌ Você não tem permissão para usar esse comando.")
        return

    cargo = discord.utils.get(ctx.guild.roles, name=nome_do_cargo)
    if not cargo:
        await ctx.send(f"❌ Cargo '{nome_do_cargo}' não encontrado.")
        return
    try:
        await membro.add_roles(cargo)
        await ctx.send(f"✅ {membro.mention} agora tem o cargo **{nome_do_cargo}** na Lumora Sync 💡")
    except discord.Forbidden:
        await ctx.send("⚠️ Não tenho permissão para dar esse cargo.")

@bot.command()
@apenas_canal_lumora()
async def help(ctx):
    texto = (
        "**📜 Comandos disponíveis da Lumora Sync:**\n"
        "`!oi` - O bot responde com uma saudação.\n"
        "`!UsoSimples <pergunta>` - Resposta da IA Simples da Lumora (🧠 segredo de fábrica).\n"
        "`!UsoAvançado <pergunta>` - Resposta inteligente com DeepSeek em tom corporativo.\n"
        "`!cargo @usuário <cargo>` - Dá um cargo (somente autorizado).\n"
        "`!help` - Mostra esta mensagem.\n"
    )
    await ctx.send(texto)

bot.run(TOKEN)
