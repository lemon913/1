import discord
from discord.ext import commands
from utils import data
import datetime
from pytz import timezone, utc
import asyncio

class support(commands.Cog):
    def __init__(self, miya):
        self.miya = miya
    
    @commands.command(name="피드백", aliases=["문의", "지원"])
    async def request(self, ctx, *args):
        """
        캐시야 피드백 < 할말 >


        개발자들 에게 피드백 메세지를 전송합니다.
        """
        channel = self.miya.get_channel(754946639474720859)
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        content = "내용 : ".join(ctx.message.content.split(" ")[2:])
        embed = discord.Embed(title="피드백이 도착했어요!", color=0x95E1F4)
        embed.add_field(name="피드백을 접수한 유저", value=f"{ctx.author} ( {ctx.author.id} )", inline=False)
        embed.add_field(name="피드백이 접수된 서버", value=f"{ctx.guild.name} ( {ctx.guild.id} )", inline=False)
        embed.add_field(name="피드백이 접수된 채널", value=f"{ctx.channel.name} ( {ctx.channel.id} )", inline=False)
        embed.add_field(name="피드백 내용", value=content, inline=False)
        embed.add_field(name="피드백 접수 완료 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
        embed.set_author(name="문의 및 답변", icon_url=self.miya.user.avatar_url)
        msg = await ctx.send(f"{ctx.author.mention} 이렇게 전송하는 게 맞나요?\n```{content}```")
        await msg.add_reaction("<:cs_yes:659355468715786262>")
        await msg.add_reaction("<:cs_no:659355468816187405>")
        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author
        try:
            reaction, user = await self.miya.wait_for('reaction_add', timeout=60, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
        else:
            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                await msg.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} 개발자에게 전송했어요! 피드백 명령어를 용도에 맞게 사용하지 않거나 이유 없이 사용하시면 봇 사용이 제한될 수 있어요.", embed=None, supress=True, delete_after=10)
                await channel.send("@everyone", embed=embed)
            else:
                await msg.delete()
    
    @commands.command(name="응답")
    @commands.is_owner()
    async def answer(self, ctx, sender: discord.User, *, response):
        """
        캐시야 응답 < 유저 > < 할말 >


        해당 유저에게 피드백에 대한 응답을 회신합니다.
        """
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        content = "내용 : " + response
        embed = discord.Embed(title="개발자가 답변을 완료했어요!", color=0x95E1F4)
        embed.add_field(name="답변의 내용", value=content, inline=False)
        embed.add_field(name="답변이 완료된 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
        embed.set_author(name="문의 및 답변", icon_url=self.miya.user.avatar_url)
        embed.set_footer(text="원하신다면 캐시야 피드백 명령어로 계속해서 문의하실 수 있어요!")
        msg = await ctx.send(f"{ctx.author.mention} 이렇게 전송하는 게 맞나요?", embed=embed)
        await msg.add_reaction("<:cs_yes:659355468715786262>")
        await msg.add_reaction("<:cs_no:659355468816187405>")
        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author
        try:
            reaction, user = await self.miya.wait_for('reaction_add', timeout=60, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
        else:
            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                try:
                    await msg.delete()
                    await sender.send(sender.mention, embed=embed)
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                except:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 해당 유저가 DM을 막아놓은 것 같아요. 전송에 실패했어요.")
            else:
                await msg.delete()
        
        

def setup(miya):
    miya.add_cog(support(miya))
