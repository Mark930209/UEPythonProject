import unreal

def get_actors_of_type(actor_class):
    """
    获取指定类型的Actor列表
    
    Args:
        actor_class: Actor类型，例如unreal.StaticMeshActor
    
    Returns:
        匹配类型的Actor列表
    """
    
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

    editor_world = editor_subsystem.get_editor_world()
    if editor_world:
        unreal.log(f"当前处于纯编辑状态")
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(editor_world, actor_class)
    else:
        unreal.log(f"当前处于PIE状态")
        pie_world = editor_subsystem.get_game_world()
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(pie_world, actor_class)
        # 方法2: 多个play实例时使用
        # worlds = unreal.EditorLevelLibrary.get_pie_worlds(False)
        # pie_world = worlds[0] if worlds else None
        
    
    # 筛选指定类型的Actor
    typed_actors = [actor for actor in all_actors if actor.get_class() == actor_class.static_class()]
    
    return typed_actors
def find_actor(actor_display_name, actor_class):
    """
    查找场景中名为Cube3的Actor，并设置其缩放
    
    Args:
        actor_display_name: Actor的显示名称，例如"TestCube"

    Returns:
        符合条件的Actor
    """
    
    actors = get_actors_of_type(actor_class)
    unreal.log(f"找到 {len(actors)} 个 {actor_class} 类型的Actor")

    target_actor = None
    for actor in actors:
        # 根据Actor名称进行筛选
        if actor.get_actor_label() == actor_display_name:
            target_actor = actor
            break
    
    return target_actor
def set_actor_scale(actor, scale):
    """
    设置Actor的缩放
    
    Args:
        actor: Actor对象
        scale: 缩放比例，unreal.Vector类型，例如unreal.Vector(10.0, 10.0, 10.0)
    """

    if actor:
        actor.set_actor_scale3d(scale)
        unreal.log(f'成功将{actor}的缩放设置为{scale}')
    else:
        unreal.log_warning("actor无效")

if __name__ == '__main__':
    target_actor = find_actor('TestCube', unreal.StaticMeshActor)
    set_actor_scale(target_actor, unreal.Vector(10.0, 10.0, 10.0))