import pachong


fuck = pachong.Pachong(name='小灰机灰上天', password='WZRJJ888')
if(fuck.status == 0):
    print("logining...")
    print(fuck.login(name='小灰机灰上天', password='WZRJJ888'))

itemid = fuck.search(keywords=['权力的游戏', '无耻家庭'])
links = fuck.get_links(itemid)
# for k, v in links:




