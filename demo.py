import pachong

fuck = pachong.Pachong(name='小灰机灰上天', password='WZRJJ888')
if(fuck.status == 0):
    print("logining...")
    print(fuck.login(name='小灰机灰上天', password='WZRJJ888'))


itemid = fuck.search(keyword='权力的游戏')
print(fuck.get_links(itemid, season=5))