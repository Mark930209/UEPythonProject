import unreal
def get_actors_of_class(actor_class):
    """
    获取指定类型的Actor列表
    
    Args:
        actor_class: Actor类型，例如unreal.StaticMeshActor，如果是unreal.Actor，则返回所有Actor
    
    Returns:
        匹配类型的Actor列表
    """
    
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

    editor_world = editor_subsystem.get_editor_world()
    if editor_world:
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(editor_world, actor_class)
        
    else:
        pie_world = editor_subsystem.get_game_world()
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(pie_world, actor_class)
        
    
    if actor_class == unreal.Actor:
        return all_actors
    
    typed_actors = [actor for actor in all_actors if actor.get_class() == actor_class or actor.get_class() == actor_class.static_class()]
    
    return typed_actors
def load_bp_class(bp_ref_path):
    """
    加载指定类名的Blueprint
    
    Args:
        class_ref_path: Blueprint的引用路径，例如'/Game/Blueprints/BP_TestActor.BP_TestActor_C'
    
    Returns:
        加载的Blueprint类
    """
    
    actor_class = unreal.load_class(None, bp_ref_path)

    if actor_class is None:
        unreal.log_warning(f"Failed to load Blueprint: {bp_ref_path}")
    else:
        unreal.log(f"Loaded Blueprint class: {actor_class}")
    
    return actor_class

def is_playing():
    """判断当前是否处于编辑器内播放状态"""
    level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    return level_editor_subsystem.is_in_play_in_editor()

def spawn_actor(actor_class, location):
    """
    生成指定类型的Actor
    
    Args:
        actor_class: Actor类型，例如unreal.StaticMeshActor
        location: Actor生成位置，unreal.Vector类型，例如unreal.Vector(100.0, 100.0, 100.0)
    
    Returns:
        生成的Actor对象
    """

    if is_playing(): # 处于编辑器内播放状态
        unreal.log_warning("当前状态无法创建，请退出编辑器内播放")
        return None
    
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    return editor_actor_subsystem.spawn_actor_from_class(actor_class, location)

def destroy_actor(actor):
    """
    销毁指定Actor
    
    Args:
        actor: Actor对象
    """
    if actor:
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        editor_actor_subsystem.destroy_actor(actor)
def bp_test():
    blueprint_path = "/Script/Engine.Blueprint'/Game/Maps/TestPythonBP.TestPythonBP_C'"
    #blueprint_path = '/Game/Maps/TestPythonBP.TestPythonBP_C'#全量引用地址和短引用地址都可以
    
    actor_class = load_bp_class(blueprint_path)
    spawned_actor = spawn_actor(actor_class, unreal.Vector(100.0, 100.0, 100.0))
    
    if spawned_actor: 
        print(spawned_actor.call_method('TestMethod'))#会按照定义的返回值类型返回一个字符串
    
    # 查找目标类型的actor
    target_actors = get_actors_of_class(actor_class)
    if target_actors[0]:
        target_actor = target_actors[0]
        # 方式1：通过元组传递参数
        target_actor.call_method('TestAdvancedMethod',(True, 11,"AdvancedMethod",['a1', 'a2' ,'a3']))
        
        # 方式2：通过字典传递参数
        args = {
            'arg1': False,
            'arg2': 12,
            'arg3': "AdvancedMethod2",
            'arg4': ['b1', 'b2' ,'b3']
        }
        target_actor.call_method('TestAdvancedMethod',(),args)
        
        #方式3：通过元组和字典混合传递参数
        args = {
            'arg3': "AdvancedMethod3",
            'arg4': ['c1', 'c2' ,'c3']
        }
        ret = target_actor.call_method('TestAdvancedMethod',(False, 13),args)
        print(ret) #因为是多个返回值，所以结果是个数组，里面有返回值
        
        destroy_actor(target_actor)
        
         
if __name__ == '__main__':
    bp_test()
    