shader_type spatial;
render_mode unshaded, cull_disabled;
uniform vec4 tint : source_color = vec4(.32,.40,.36,1);
varying vec3 world_position;
varying vec3 world_normal;
void vertex() {
	world_position=(MODEL_MATRIX*vec4(VERTEX,1)).xyz;
	world_normal=normalize(MODEL_NORMAL_MATRIX*NORMAL);
}
void fragment() {
	float ridge=.5+.5*sin(world_position.x*.19+world_position.y*.44+sin(world_position.z*.17)*2.0);
	float slope=clamp(world_normal.y,0.0,1.0);
	float side=.50+.40*max(dot(normalize(world_normal),normalize(vec3(-.82,.48,.29))),0.0);
	vec3 rock=mix(tint.rgb*.66,tint.rgb*1.25,ridge*.30+slope*.45);
	ALBEDO=rock*side;
}
